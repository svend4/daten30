import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';

void main() => runApp(DynamicHubApp());

class DynamicHubApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Dynamic Hub',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: HubHomeScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

// ============= MODELS =============

class MicroService {
  final String id;
  final String name;
  final String? description;
  final int port;
  final String status;
  final String? icon;
  final String? color;
  final String? category;
  final Map<String, dynamic>? uiSchema;

  MicroService({
    required this.id,
    required this.name,
    this.description,
    required this.port,
    required this.status,
    this.icon,
    this.color,
    this.category,
    this.uiSchema,
  });

  factory MicroService.fromJson(Map<String, dynamic> json) {
    return MicroService(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      port: json['port'],
      status: json['status'] ?? 'active',
      icon: json['icon'],
      color: json['color'],
      category: json['category'],
      uiSchema: json['ui_schema'] is String
          ? jsonDecode(json['ui_schema'])
          : json['ui_schema'],
    );
  }
}

// ============= SERVICE DISCOVERY =============

class ServiceDiscovery {
  static const String registryUrl = 'http://127.0.0.1:5000';

  Future<List<MicroService>> discoverServices() async {
    try {
      final response = await http.get(
        Uri.parse('$registryUrl/api/services'),
      ).timeout(Duration(seconds: 5));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        if (data['success'] == true && data['services'] != null) {
          return (data['services'] as List)
              .map((s) => MicroService.fromJson(s))
              .toList();
        }
      }

      return [];
    } catch (e) {
      print('Error discovering services: $e');
      return [];
    }
  }

  Future<bool> checkRegistryHealth() async {
    try {
      final response = await http.get(
        Uri.parse('$registryUrl/health'),
      ).timeout(Duration(seconds: 2));

      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}

// ============= HOME SCREEN =============

class HubHomeScreen extends StatefulWidget {
  @override
  _HubHomeScreenState createState() => _HubHomeScreenState();
}

class _HubHomeScreenState extends State<HubHomeScreen> {
  final ServiceDiscovery _discovery = ServiceDiscovery();
  List<MicroService> services = [];
  bool loading = true;
  bool registryAvailable = false;
  String? error;
  Timer? _autoRefreshTimer;

  @override
  void initState() {
    super.initState();
    discoverServices();

    // Автообновление каждые 30 секунд
    _autoRefreshTimer = Timer.periodic(
      Duration(seconds: 30),
      (_) => discoverServices(),
    );
  }

  @override
  void dispose() {
    _autoRefreshTimer?.cancel();
    super.dispose();
  }

  Future<void> discoverServices() async {
    setState(() {
      loading = true;
      error = null;
    });

    try {
      // Проверить доступность Registry
      final healthCheck = await _discovery.checkRegistryHealth();

      if (!healthCheck) {
        setState(() {
          loading = false;
          registryAvailable = false;
          error = 'Service Registry недоступен';
        });
        return;
      }

      // Получить список сервисов
      final discoveredServices = await _discovery.discoverServices();

      setState(() {
        services = discoveredServices;
        loading = false;
        registryAvailable = true;
      });

      if (discoveredServices.isEmpty) {
        setState(() {
          error = 'Нет доступных сервисов';
        });
      }

    } catch (e) {
      setState(() {
        loading = false;
        error = 'Ошибка: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dynamic Hub'),
        actions: [
          // Индикатор подключения
          Padding(
            padding: EdgeInsets.only(right: 8),
            child: Center(
              child: Container(
                padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: registryAvailable ? Colors.green : Colors.red,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      registryAvailable ? Icons.check_circle : Icons.error,
                      size: 16,
                      color: Colors.white,
                    ),
                    SizedBox(width: 4),
                    Text(
                      registryAvailable ? 'Online' : 'Offline',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: discoverServices,
            tooltip: 'Обновить',
          ),
        ],
      ),
      body: loading
          ? Center(child: CircularProgressIndicator())
          : _buildBody(),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: discoverServices,
        label: Text('Обновить'),
        icon: Icon(Icons.refresh),
      ),
    );
  }

  Widget _buildBody() {
    // Если Registry недоступен
    if (!registryAvailable) {
      return _buildErrorCard(
        'Service Registry недоступен',
        'Убедитесь что Service Registry запущен:',
        [
          'cd ~/daten30/hub-portal',
          'bash scripts/start-all.sh',
        ],
      );
    }

    // Если нет сервисов
    if (services.isEmpty) {
      return _buildErrorCard(
        'Нет доступных сервисов',
        'Запустите микросервисы:',
        [
          'cd ~/daten30/hub-portal',
          'bash scripts/start-all.sh',
        ],
      );
    }

    // Показать сервисы
    return RefreshIndicator(
      onRefresh: discoverServices,
      child: CustomScrollView(
        slivers: [
          // Статистика
          SliverToBoxAdapter(
            child: Padding(
              padding: EdgeInsets.all(16),
              child: Card(
                child: Padding(
                  padding: EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Доступные сервисы',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      SizedBox(height: 8),
                      Text(
                        '${services.length} ${_pluralize(services.length, 'сервис', 'сервиса', 'сервисов')}',
                        style: Theme.of(context).textTheme.bodyLarge,
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),

          // Сетка карточек сервисов
          SliverPadding(
            padding: EdgeInsets.all(16),
            sliver: SliverGrid(
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
                childAspectRatio: 1.0,
              ),
              delegate: SliverChildBuilderDelegate(
                (context, index) {
                  final service = services[index];
                  return ServiceCard(
                    service: service,
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => DynamicServiceScreen(
                            service: service,
                          ),
                        ),
                      );
                    },
                  );
                },
                childCount: services.length,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildErrorCard(String title, String subtitle, List<String> commands) {
    return Center(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Card(
          color: Colors.red.shade50,
          child: Padding(
            padding: EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.error_outline, size: 64, color: Colors.red),
                SizedBox(height: 16),
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Colors.red.shade900,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 8),
                Text(
                  subtitle,
                  style: TextStyle(fontSize: 16),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 16),
                Container(
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.black87,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: commands.map((cmd) =>
                      Padding(
                        padding: EdgeInsets.symmetric(vertical: 2),
                        child: Text(
                          cmd,
                          style: TextStyle(
                            fontFamily: 'monospace',
                            color: Colors.green.shade300,
                          ),
                        ),
                      )
                    ).toList(),
                  ),
                ),
                SizedBox(height: 16),
                ElevatedButton.icon(
                  onPressed: discoverServices,
                  icon: Icon(Icons.refresh),
                  label: Text('Попробовать снова'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  String _pluralize(int count, String one, String two, String many) {
    if (count % 10 == 1 && count % 100 != 11) return one;
    if (count % 10 >= 2 && count % 10 <= 4 && (count % 100 < 10 || count % 100 >= 20)) return two;
    return many;
  }
}

// ============= SERVICE CARD =============

class ServiceCard extends StatelessWidget {
  final MicroService service;
  final VoidCallback onTap;

  const ServiceCard({required this.service, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                _getIconData(service.icon),
                size: 48,
                color: _parseColor(service.color),
              ),
              SizedBox(height: 12),
              Text(
                service.name,
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              if (service.description != null) ...[
                SizedBox(height: 4),
                Text(
                  service.description!,
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey,
                  ),
                  textAlign: TextAlign.center,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
              SizedBox(height: 8),
              Container(
                padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: _parseColor(service.color).withOpacity(0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  'Port ${service.port}',
                  style: TextStyle(
                    fontSize: 10,
                    color: _parseColor(service.color),
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  IconData _getIconData(String? iconName) {
    switch (iconName) {
      case 'shopping_cart':
        return Icons.shopping_cart;
      case 'wb_sunny':
        return Icons.wb_sunny;
      case 'currency_bitcoin':
        return Icons.currency_bitcoin;
      case 'article':
        return Icons.article;
      case 'task_alt':
        return Icons.task_alt;
      default:
        return Icons.widgets;
    }
  }

  Color _parseColor(String? colorHex) {
    if (colorHex == null) return Colors.blue;
    try {
      return Color(int.parse(colorHex.replaceFirst('#', '0xFF')));
    } catch (e) {
      return Colors.blue;
    }
  }
}

// ============= DYNAMIC SERVICE SCREEN =============

class DynamicServiceScreen extends StatefulWidget {
  final MicroService service;

  const DynamicServiceScreen({required this.service});

  @override
  _DynamicServiceScreenState createState() => _DynamicServiceScreenState();
}

class _DynamicServiceScreenState extends State<DynamicServiceScreen> {
  Map<String, dynamic>? data;
  bool loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    loadData();
  }

  Future<void> loadData() async {
    setState(() {
      loading = true;
      error = null;
    });

    final endpoint = widget.service.uiSchema?['endpoint'] ?? '/api/data';
    final url = 'http://127.0.0.1:${widget.service.port}$endpoint';

    try {
      final response = await http.get(Uri.parse(url)).timeout(
        Duration(seconds: 5),
      );

      if (response.statusCode == 200) {
        setState(() {
          data = json.decode(response.body);
          loading = false;
        });
      } else {
        throw Exception('HTTP ${response.statusCode}');
      }
    } catch (e) {
      setState(() {
        loading = false;
        error = 'Ошибка загрузки: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.service.name),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: loadData,
          ),
        ],
      ),
      body: loading
          ? Center(child: CircularProgressIndicator())
          : error != null
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.error, size: 64, color: Colors.red),
                      SizedBox(height: 16),
                      Text(error!),
                      SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: loadData,
                        child: Text('Попробовать снова'),
                      ),
                    ],
                  ),
                )
              : data == null
                  ? Center(child: Text('Нет данных'))
                  : DynamicWidgetBuilder().build(
                      widget.service.uiSchema ?? {},
                      data!,
                    ),
    );
  }
}

// ============= DYNAMIC WIDGET BUILDER =============

class DynamicWidgetBuilder {
  Widget build(Map<String, dynamic> schema, Map<String, dynamic> data) {
    final type = schema['type'];

    switch (type) {
      case 'list':
        return _buildList(schema, data);
      case 'card':
        return _buildCard(schema, data);
      case 'grid':
        return _buildGrid(schema, data);
      default:
        return _buildList(schema, data);
    }
  }

  Widget _buildList(Map<String, dynamic> schema, Map<String, dynamic> data) {
    // Попытаться найти массив данных
    List items = [];

    if (data['products'] != null) {
      items = data['products'];
    } else if (data['prices'] != null) {
      items = data['prices'];
    } else if (data['news'] != null) {
      items = data['news'];
    } else if (data['tasks'] != null) {
      items = data['tasks'];
    } else if (data['items'] != null) {
      items = data['items'];
    }

    if (items.isEmpty) {
      return Center(child: Text('Нет данных для отображения'));
    }

    final template = schema['item_template'] ?? {};

    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (context, index) {
        final item = items[index];
        return _buildListItem(template, item);
      },
    );
  }

  Widget _buildListItem(Map<String, dynamic> template, Map<String, dynamic> item) {
    return Card(
      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: ListTile(
        title: Text(_interpolate(template['title'] ?? '', item)),
        subtitle: Text(_interpolate(template['subtitle'] ?? '', item)),
        trailing: template['badge'] != null
            ? Chip(
                label: Text(_interpolate(template['badge'], item)),
              )
            : null,
      ),
    );
  }

  Widget _buildCard(Map<String, dynamic> schema, Map<String, dynamic> data) {
    return Center(
      child: Card(
        margin: EdgeInsets.all(16),
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                _interpolate(schema['title'] ?? '', data),
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 8),
              Text(
                _interpolate(schema['subtitle'] ?? '', data),
                style: TextStyle(fontSize: 18),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildGrid(Map<String, dynamic> schema, Map<String, dynamic> data) {
    List items = data['items'] ?? [];

    return GridView.builder(
      padding: EdgeInsets.all(16),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: schema['columns'] ?? 2,
        crossAxisSpacing: 16,
        mainAxisSpacing: 16,
      ),
      itemCount: items.length,
      itemBuilder: (context, index) {
        final item = items[index];
        final template = schema['item_template'] ?? {};

        return Card(
          child: Padding(
            padding: EdgeInsets.all(12),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  _interpolate(template['title'] ?? '', item),
                  style: TextStyle(fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 4),
                Text(
                  _interpolate(template['subtitle'] ?? '', item),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  String _interpolate(String template, Map<String, dynamic> data) {
    String result = template;
    final regex = RegExp(r'\{\{(\w+)\}\}');

    result = result.replaceAllMapped(regex, (match) {
      final key = match.group(1);
      return data[key]?.toString() ?? '';
    });

    return result;
  }
}
