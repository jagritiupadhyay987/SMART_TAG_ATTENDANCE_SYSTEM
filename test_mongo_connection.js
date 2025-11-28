const { MongoClient } = require('mongodb');

async function testConnection() {
    const uri = 'mongodb://localhost:27017/';
    const client = new MongoClient(uri);
    
    try {
        console.log('Testing MongoDB connection...');
        await client.connect();
        console.log('✅ Connected to MongoDB successfully!');
        
        // Test ping
        await client.db('admin').command({ ping: 1 });
        console.log('✅ MongoDB ping successful!');
        
        // List databases
        const databases = await client.db().admin().listDatabases();
        console.log('Available databases:', databases.databases.map(db => db.name));
        
        // Test creating a test database
        const testDb = client.db('test_connection');
        const testCollection = testDb.collection('test');
        
        // Insert a test document
        const result = await testCollection.insertOne({ test: 'connection', timestamp: new Date() });
        console.log('✅ Test document inserted with ID:', result.insertedId);
        
        // Find the document
        const foundDoc = await testCollection.findOne({ test: 'connection' });
        console.log('✅ Test document found:', foundDoc);
        
        // Clean up
        await testCollection.drop();
        await testDb.dropDatabase();
        console.log('✅ Test database cleaned up');
        
    } catch (error) {
        console.error('❌ MongoDB connection failed:', error.message);
        process.exit(1);
    } finally {
        await client.close();
        console.log('✅ Connection closed');
    }
}

testConnection();
