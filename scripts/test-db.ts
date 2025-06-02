import { PrismaClient } from '@prisma/client';

async function main() {
  const prisma = new PrismaClient();
  
  try {
    // Test the connection
    await prisma.$connect();
    console.log('✅ Successfully connected to the database');

    // Try to create a test user
    const testUser = await prisma.user.create({
      data: {
        email: 'test@example.com',
        name: 'Test User',
      },
    });
    console.log('✅ Successfully created a test user:', testUser);

    // Try to read the user back
    const readUser = await prisma.user.findUnique({
      where: { email: 'test@example.com' },
    });
    console.log('✅ Successfully read the test user:', readUser);

    // Clean up - delete the test user
    await prisma.user.delete({
      where: { email: 'test@example.com' },
    });
    console.log('✅ Successfully cleaned up test data');

  } catch (error) {
    console.error('❌ Error:', error);
  } finally {
    await prisma.$disconnect();
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  }); 