// Run with the required passwords supplied by the shell environment.
const adminPassword = process.env.MONGO_ADMIN_PASSWORD;
const appPassword = process.env.MONGO_APP_PASSWORD;

if (!adminPassword || !appPassword) {
  throw new Error('Set MONGO_ADMIN_PASSWORD and MONGO_APP_PASSWORD before running this script.');
}

// 连接到 admin 数据库
const adminDb = db.getSiblingDB('admin');

// 创建或更新管理员用户
adminDb.createUser({
  user: 'admin',
  pwd: adminPassword,
  roles: [{ role: 'root', db: 'admin' }]
});

// 创建应用数据库用户
adminDb.createUser({
  user: 'mongo',
  pwd: appPassword,
  roles: [
    { role: 'readWrite', db: 'douyin_analysis' },
    { role: 'read', db: 'local' }
  ]
});

print('Users created successfully');