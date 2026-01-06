import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// API Configuration для разных режимов
class ApiConfig {
  // Режим работы: 'termux', 'online', 'emulator'
  static const String mode = 'termux'; // ← Измените здесь!

  // Termux режим (Flask на том же устройстве)
  static const String _termuxUserService = 'http://127.0.0.1:5001';
  static const String _termuxProductService = 'http://127.0.0.1:5002';
  static const String _termuxOrderService = 'http://127.0.0.1:5003';

  // Online режим (Backend на сервере)
  static const String _onlineBaseUrl = 'http://YOUR_SERVER:8080/api';

  // Emulator режим (для тестирования в эмуляторе)
  static const String _emulatorBaseUrl = 'http://10.0.2.2:8080/api';

  // Получить URL для Users
  static String get userServiceUrl {
    switch (mode) {
      case 'termux':
        return '$_termuxUserService/api/users';
      case 'online':
        return '$_onlineBaseUrl/users';
      case 'emulator':
        return '$_emulatorBaseUrl/users';
      default:
        return '$_termuxUserService/api/users';
    }
  }

  // Получить URL для Products
  static String get productServiceUrl {
    switch (mode) {
      case 'termux':
        return '$_termuxProductService/api/products';
      case 'online':
        return '$_onlineBaseUrl/products';
      case 'emulator':
        return '$_emulatorBaseUrl/products';
      default:
        return '$_termuxProductService/api/products';
    }
  }

  // Получить URL для Orders
  static String get orderServiceUrl {
    switch (mode) {
      case 'termux':
        return '$_termuxOrderService/api/orders';
      case 'online':
        return '$_onlineBaseUrl/orders';
      case 'emulator':
        return '$_emulatorBaseUrl/orders';
      default:
        return '$_termuxOrderService/api/orders';
    }
  }

  // Health check URLs
  static String get userHealthUrl => mode == 'termux'
      ? '$_termuxUserService/health'
      : '$_onlineBaseUrl/users/health';
  static String get productHealthUrl => mode == 'termux'
      ? '$_termuxProductService/health'
      : '$_onlineBaseUrl/products/health';
  static String get orderHealthUrl => mode == 'termux'
      ? '$_termuxOrderService/health'
      : '$_onlineBaseUrl/orders/health';
}

// API Service с поддержкой разных endpoints
class ApiService {
  Future<Map<String, dynamic>> get(String url) async {
    try {
      final response = await http.get(Uri.parse(url));
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      throw Exception('HTTP ${response.statusCode}: ${response.body}');
    } catch (e) {
      throw Exception('Failed to load data: $e');
    }
  }

  Future<Map<String, dynamic>> post(String url, Map<String, dynamic> data) async {
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        return json.decode(response.body);
      }
      throw Exception('HTTP ${response.statusCode}: ${response.body}');
    } catch (e) {
      throw Exception('Failed to post data: $e');
    }
  }
}

// Data Provider
class DataProvider with ChangeNotifier {
  final ApiService _api = ApiService();

  List<dynamic> users = [];
  List<dynamic> products = [];
  List<dynamic> orders = [];
  Map<String, dynamic> stats = {};
  bool isLoading = false;
  String? error;

  Future<void> loadUsers() async {
    isLoading = true;
    notifyListeners();
    try {
      final data = await _api.get(ApiConfig.userServiceUrl);
      users = data['users'] ?? [];
      error = null;
    } catch (e) {
      error = e.toString();
    }
    isLoading = false;
    notifyListeners();
  }

  Future<void> loadProducts() async {
    isLoading = true;
    notifyListeners();
    try {
      final data = await _api.get(ApiConfig.productServiceUrl);
      products = data['products'] ?? [];
      error = null;
    } catch (e) {
      error = e.toString();
    }
    isLoading = false;
    notifyListeners();
  }

  Future<void> loadOrders() async {
    isLoading = true;
    notifyListeners();
    try {
      final data = await _api.get(ApiConfig.orderServiceUrl);
      orders = data['orders'] ?? [];
      error = null;
    } catch (e) {
      error = e.toString();
    }
    isLoading = false;
    notifyListeners();
  }

  Future<void> loadStats() async {
    try {
      final userStats = await _api.get('/user-stats');
      final productStats = await _api.get('/product-stats');
      final orderStats = await _api.get('/order-stats');
      stats = {
        'users': userStats['total_users'] ?? 0,
        'products': productStats['total_products'] ?? 0,
        'orders': orderStats['total_orders'] ?? 0,
      };
      notifyListeners();
    } catch (e) {
      error = e.toString();
    }
  }
}

// Main App
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => DataProvider(),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Demo App - Flutter',
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}

// Home Screen with Bottom Navigation
class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  final List<Widget> _screens = const [
    DashboardScreen(),
    UsersScreen(),
    ProductsScreen(),
    OrdersScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🚀 Demo App - Flutter'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.dashboard), label: 'Dashboard'),
          BottomNavigationBarItem(icon: Icon(Icons.people), label: 'Users'),
          BottomNavigationBarItem(icon: Icon(Icons.shopping_bag), label: 'Products'),
          BottomNavigationBarItem(icon: Icon(Icons.receipt), label: 'Orders'),
        ],
      ),
    );
  }
}

// Dashboard Screen
class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<DataProvider>().loadStats();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<DataProvider>(
      builder: (context, provider, child) {
        return SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Termux Connection Status
              if (provider.error != null)
                Card(
                  color: Colors.red.shade50,
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(Icons.error_outline, color: Colors.red),
                            SizedBox(width: 8),
                            Text('❌ Нет связи с Termux', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.red)),
                          ],
                        ),
                        SizedBox(height: 8),
                        Text('Убедитесь что Termux backend запущен:', style: TextStyle(fontSize: 12)),
                        SizedBox(height: 4),
                        Text('cd ~/daten30/termux', style: TextStyle(fontSize: 11, fontFamily: 'monospace')),
                        Text('bash scripts/start-all.sh', style: TextStyle(fontSize: 11, fontFamily: 'monospace')),
                        SizedBox(height: 12),
                        ElevatedButton.icon(
                          onPressed: provider.isLoading ? null : () {
                            context.read<DataProvider>().loadStats();
                            context.read<DataProvider>().loadUsers();
                            context.read<DataProvider>().loadProducts();
                            context.read<DataProvider>().loadOrders();
                          },
                          icon: Icon(Icons.refresh),
                          label: Text('🔄 Повторить подключение'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.orange,
                            foregroundColor: Colors.white,
                          ),
                        ),
                      ],
                    ),
                  ),
                )
              else
                Card(
                  color: Colors.green.shade50,
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Row(
                      children: [
                        Icon(Icons.check_circle, color: Colors.green, size: 20),
                        SizedBox(width: 8),
                        Text('✅ Подключено к Termux', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.green)),
                        Spacer(),
                        IconButton(
                          icon: Icon(Icons.refresh, color: Colors.green),
                          onPressed: provider.isLoading ? null : () {
                            context.read<DataProvider>().loadStats();
                            context.read<DataProvider>().loadUsers();
                            context.read<DataProvider>().loadProducts();
                            context.read<DataProvider>().loadOrders();
                          },
                        ),
                      ],
                    ),
                  ),
                ),
              const SizedBox(height: 20),
              const Text('📊 System Overview', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
              const SizedBox(height: 20),
              Row(
                children: [
                  Expanded(child: _buildStatCard('👥', 'Users', provider.stats['users']?.toString() ?? '0', Colors.blue)),
                  const SizedBox(width: 10),
                  Expanded(child: _buildStatCard('🛍️', 'Products', provider.stats['products']?.toString() ?? '0', Colors.green)),
                ],
              ),
              const SizedBox(height: 10),
              Row(
                children: [
                  Expanded(child: _buildStatCard('📦', 'Orders', provider.stats['orders']?.toString() ?? '0', Colors.orange)),
                  const SizedBox(width: 10),
                  Expanded(child: Container()),
                ],
              ),
              const SizedBox(height: 30),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('🎯 Architecture Highlights', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 10),
                      _buildInfoRow('Microservices', 'User, Product, Order, Analytics, Notification'),
                      _buildInfoRow('Polyglot Persistence', 'MongoDB + PostgreSQL + Redis + Cassandra'),
                      _buildInfoRow('Mobile', 'Flutter (iOS + Android + Web)'),
                      _buildInfoRow('Backend', 'Flask (Python) + Gin (Go) + Fastify (Node.js)'),
                    ],
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildStatCard(String icon, String label, String value, Color color) {
    return Card(
      color: color.withOpacity(0.1),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Text(icon, style: const TextStyle(fontSize: 40)),
            const SizedBox(height: 10),
            Text(value, style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: color)),
            Text(label, style: TextStyle(fontSize: 14, color: color)),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('$label: ', style: const TextStyle(fontWeight: FontWeight.bold)),
          Expanded(child: Text(value)),
        ],
      ),
    );
  }
}

// Users Screen
class UsersScreen extends StatefulWidget {
  const UsersScreen({super.key});

  @override
  State<UsersScreen> createState() => _UsersScreenState();
}

class _UsersScreenState extends State<UsersScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<DataProvider>().loadUsers();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<DataProvider>(
      builder: (context, provider, child) {
        if (provider.isLoading) {
          return const Center(child: CircularProgressIndicator());
        }
        if (provider.error != null) {
          return Center(
            child: Padding(
              padding: const EdgeInsets.all(32),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.error_outline, size: 64, color: Colors.red),
                  SizedBox(height: 16),
                  Text('Ошибка подключения', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                  SizedBox(height: 8),
                  Text('Убедитесь что Termux backend запущен', textAlign: TextAlign.center),
                  SizedBox(height: 24),
                  ElevatedButton.icon(
                    onPressed: () => context.read<DataProvider>().loadUsers(),
                    icon: Icon(Icons.refresh),
                    label: Text('Повторить'),
                  ),
                ],
              ),
            ),
          );
        }
        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: provider.users.length,
          itemBuilder: (context, index) {
            final user = provider.users[index];
            return Card(
              margin: const EdgeInsets.only(bottom: 12),
              child: ListTile(
                leading: CircleAvatar(
                  child: Text(user['name'][0].toUpperCase()),
                ),
                title: Text(user['name']),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(user['email']),
                    Text('Role: ${user['role']}', style: const TextStyle(fontSize: 12)),
                  ],
                ),
                isThreeLine: true,
              ),
            );
          },
        );
      },
    );
  }
}

// Products Screen
class ProductsScreen extends StatefulWidget {
  const ProductsScreen({super.key});

  @override
  State<ProductsScreen> createState() => _ProductsScreenState();
}

class _ProductsScreenState extends State<ProductsScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<DataProvider>().loadProducts();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<DataProvider>(
      builder: (context, provider, child) {
        if (provider.isLoading) {
          return const Center(child: CircularProgressIndicator());
        }
        if (provider.error != null) {
          return Center(
            child: Padding(
              padding: const EdgeInsets.all(32),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.error_outline, size: 64, color: Colors.red),
                  SizedBox(height: 16),
                  Text('Ошибка подключения', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                  SizedBox(height: 8),
                  Text('Убедитесь что Termux backend запущен', textAlign: TextAlign.center),
                  SizedBox(height: 24),
                  ElevatedButton.icon(
                    onPressed: () => context.read<DataProvider>().loadProducts(),
                    icon: Icon(Icons.refresh),
                    label: Text('Повторить'),
                  ),
                ],
              ),
            ),
          );
        }
        return GridView.builder(
          padding: const EdgeInsets.all(16),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            childAspectRatio: 0.75,
            crossAxisSpacing: 10,
            mainAxisSpacing: 10,
          ),
          itemCount: provider.products.length,
          itemBuilder: (context, index) {
            final product = provider.products[index];
            return Card(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(product['name'], style: const TextStyle(fontWeight: FontWeight.bold), maxLines: 2, overflow: TextOverflow.ellipsis),
                    const SizedBox(height: 8),
                    Chip(label: Text(product['category'], style: const TextStyle(fontSize: 10)), padding: EdgeInsets.zero),
                    const Spacer(),
                    Text('${product['price']} ₽', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.deepPurple)),
                    Text('Stock: ${product['stock']}', style: const TextStyle(fontSize: 12, color: Colors.grey)),
                  ],
                ),
              ),
            );
          },
        );
      },
    );
  }
}

// Orders Screen
class OrdersScreen extends StatefulWidget {
  const OrdersScreen({super.key});

  @override
  State<OrdersScreen> createState() => _OrdersScreenState();
}

class _OrdersScreenState extends State<OrdersScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<DataProvider>().loadOrders();
    });
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'delivered': return Colors.green;
      case 'shipped': return Colors.purple;
      case 'processing': return Colors.blue;
      case 'cancelled': return Colors.red;
      default: return Colors.orange;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<DataProvider>(
      builder: (context, provider, child) {
        if (provider.isLoading) {
          return const Center(child: CircularProgressIndicator());
        }
        if (provider.error != null) {
          return Center(
            child: Padding(
              padding: const EdgeInsets.all(32),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.error_outline, size: 64, color: Colors.red),
                  SizedBox(height: 16),
                  Text('Ошибка подключения', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                  SizedBox(height: 8),
                  Text('Убедитесь что Termux backend запущен', textAlign: TextAlign.center),
                  SizedBox(height: 24),
                  ElevatedButton.icon(
                    onPressed: () => context.read<DataProvider>().loadOrders(),
                    icon: Icon(Icons.refresh),
                    label: Text('Повторить'),
                  ),
                ],
              ),
            ),
          );
        }
        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: provider.orders.length,
          itemBuilder: (context, index) {
            final order = provider.orders[index];
            return Card(
              margin: const EdgeInsets.only(bottom: 12),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Order #${order['id']}', style: const TextStyle(fontWeight: FontWeight.bold)),
                        Chip(
                          label: Text(order['status'], style: const TextStyle(color: Colors.white, fontSize: 12)),
                          backgroundColor: _getStatusColor(order['status']),
                          padding: const EdgeInsets.symmetric(horizontal: 8),
                        ),
                      ],
                    ),
                    const Divider(),
                    Text('User ID: ${order['user_id']}'),
                    const SizedBox(height: 4),
                    Text('Total: ${order['total_amount']} ₽', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.deepPurple)),
                  ],
                ),
              ),
            );
          },
        );
      },
    );
  }
}
