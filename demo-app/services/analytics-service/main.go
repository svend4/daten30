// Analytics Service - Gin (Go)
// Философия: Высокопроизводительный сервис аналитики
// Использует Cassandra для хранения временных рядов и Kafka для получения событий

package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/gocql/gocql"
	"github.com/segmentio/kafka-go"
)

var (
	cassandraSession *gocql.Session
	kafkaReader      *kafka.Reader
)

// Event структура для событий из Kafka
type Event struct {
	EventType string                 `json:"event_type"`
	Timestamp time.Time              `json:"timestamp"`
	Data      map[string]interface{} `json:"data"`
}

// Analytics структура для аналитических данных
type Analytics struct {
	EventType string    `json:"event_type"`
	Count     int64     `json:"count"`
	Day       time.Time `json:"day"`
}

func main() {
	// Инициализация Cassandra
	if err := initCassandra(); err != nil {
		log.Fatalf("Failed to connect to Cassandra: %v", err)
	}
	defer cassandraSession.Close()

	// Инициализация Kafka consumer
	initKafka()
	defer kafkaReader.Close()

	// Запуск Kafka consumer в отдельной горутине
	go consumeKafkaEvents()

	// Настройка Gin router
	router := gin.Default()

	// Health check
	router.GET("/health", healthCheck)

	// Analytics endpoints
	router.GET("/analytics/summary", getAnalyticsSummary)
	router.GET("/analytics/events", getEventsByType)
	router.GET("/analytics/daily", getDailyStats)

	// Запуск сервера
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Analytics Service starting on port %s", port)
	router.Run(":" + port)
}

// initCassandra инициализирует подключение к Cassandra
func initCassandra() error {
	cassandraHost := os.Getenv("CASSANDRA_HOST")
	if cassandraHost == "" {
		cassandraHost = "cassandra-client"
	}

	cluster := gocql.NewCluster(cassandraHost)
	cluster.Consistency = gocql.Quorum
	cluster.Timeout = 10 * time.Second

	var err error
	cassandraSession, err = cluster.CreateSession()
	if err != nil {
		return err
	}

	// Создание keyspace и таблиц
	if err := createSchema(); err != nil {
		return err
	}

	log.Println("Connected to Cassandra")
	return nil
}

// createSchema создаёт keyspace и таблицы
func createSchema() error {
	// Создание keyspace
	if err := cassandraSession.Query(`
		CREATE KEYSPACE IF NOT EXISTS analytics
		WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
	`).Exec(); err != nil {
		return err
	}

	// Создание таблицы events
	if err := cassandraSession.Query(`
		CREATE TABLE IF NOT EXISTS analytics.events (
			event_id uuid PRIMARY KEY,
			event_type text,
			timestamp timestamp,
			data text
		)
	`).Exec(); err != nil {
		return err
	}

	// Создание таблицы daily_stats
	if err := cassandraSession.Query(`
		CREATE TABLE IF NOT EXISTS analytics.daily_stats (
			event_type text,
			day date,
			count counter,
			PRIMARY KEY (event_type, day)
		)
	`).Exec(); err != nil {
		return err
	}

	log.Println("Cassandra schema created")
	return nil
}

// initKafka инициализирует Kafka consumer
func initKafka() {
	kafkaBroker := os.Getenv("KAFKA_BROKER")
	if kafkaBroker == "" {
		kafkaBroker = "kafka-service:9092"
	}

	kafkaReader = kafka.NewReader(kafka.ReaderConfig{
		Brokers:  []string{kafkaBroker},
		Topic:    "app-events",
		GroupID:  "analytics-service",
		MinBytes: 10e3, // 10KB
		MaxBytes: 10e6, // 10MB
	})

	log.Println("Kafka consumer initialized")
}

// consumeKafkaEvents потребляет события из Kafka
func consumeKafkaEvents() {
	log.Println("Starting Kafka event consumer")

	for {
		msg, err := kafkaReader.ReadMessage(context.Background())
		if err != nil {
			log.Printf("Error reading Kafka message: %v", err)
			continue
		}

		var event Event
		if err := json.Unmarshal(msg.Value, &event); err != nil {
			log.Printf("Error unmarshaling event: %v", err)
			continue
		}

		// Сохранение события в Cassandra
		if err := saveEvent(event); err != nil {
			log.Printf("Error saving event: %v", err)
		}

		log.Printf("Processed event: %s", event.EventType)
	}
}

// saveEvent сохраняет событие в Cassandra
func saveEvent(event Event) error {
	// Сохранение события
	dataJSON, _ := json.Marshal(event.Data)
	eventID := gocql.TimeUUID()

	if err := cassandraSession.Query(`
		INSERT INTO analytics.events (event_id, event_type, timestamp, data)
		VALUES (?, ?, ?, ?)
	`, eventID, event.EventType, event.Timestamp, string(dataJSON)).Exec(); err != nil {
		return err
	}

	// Обновление дневной статистики
	day := time.Date(event.Timestamp.Year(), event.Timestamp.Month(), event.Timestamp.Day(), 0, 0, 0, 0, time.UTC)
	if err := cassandraSession.Query(`
		UPDATE analytics.daily_stats
		SET count = count + 1
		WHERE event_type = ? AND day = ?
	`, event.EventType, day).Exec(); err != nil {
		return err
	}

	return nil
}

// healthCheck проверяет здоровье сервиса
func healthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "healthy",
		"service": "analytics-service",
		"timestamp": time.Now(),
	})
}

// getAnalyticsSummary возвращает общую статистику
func getAnalyticsSummary(c *gin.Context) {
	var stats []Analytics

	iter := cassandraSession.Query(`
		SELECT event_type, day, count
		FROM analytics.daily_stats
	`).Iter()

	var eventType string
	var day time.Time
	var count int64

	for iter.Scan(&eventType, &day, &count) {
		stats = append(stats, Analytics{
			EventType: eventType,
			Count:     count,
			Day:       day,
		})
	}

	if err := iter.Close(); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"summary": stats,
		"total_records": len(stats),
	})
}

// getEventsByType возвращает события по типу
func getEventsByType(c *gin.Context) {
	eventType := c.Query("type")
	if eventType == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "event type required"})
		return
	}

	var events []map[string]interface{}

	iter := cassandraSession.Query(`
		SELECT event_id, event_type, timestamp, data
		FROM analytics.events
		WHERE event_type = ?
		ALLOW FILTERING
	`, eventType).Iter()

	var eventID gocql.UUID
	var eType string
	var timestamp time.Time
	var data string

	for iter.Scan(&eventID, &eType, &timestamp, &data) {
		var dataMap map[string]interface{}
		json.Unmarshal([]byte(data), &dataMap)

		events = append(events, map[string]interface{}{
			"event_id":   eventID.String(),
			"event_type": eType,
			"timestamp":  timestamp,
			"data":       dataMap,
		})
	}

	if err := iter.Close(); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"events": events,
		"count":  len(events),
	})
}

// getDailyStats возвращает дневную статистику
func getDailyStats(c *gin.Context) {
	var stats []Analytics

	iter := cassandraSession.Query(`
		SELECT event_type, day, count
		FROM analytics.daily_stats
	`).Iter()

	var eventType string
	var day time.Time
	var count int64

	for iter.Scan(&eventType, &day, &count) {
		stats = append(stats, Analytics{
			EventType: eventType,
			Count:     count,
			Day:       day,
		})
	}

	if err := iter.Close(); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"daily_stats": stats,
		"count":       len(stats),
	})
}
