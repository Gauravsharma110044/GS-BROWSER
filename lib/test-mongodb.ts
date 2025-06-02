import clientPromise from './mongodb';

export async function testConnection() {
  try {
    const client = await clientPromise;
    const db = client.db("test");
    
    // Test the connection
    await db.command({ ping: 1 });
    console.log("Successfully connected to MongoDB.");
    
    return true;
  } catch (error) {
    console.error("Error connecting to MongoDB:", error);
    return false;
  }
} 