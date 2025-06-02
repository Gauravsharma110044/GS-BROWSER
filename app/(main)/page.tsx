import { useSession } from 'next-auth/react';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

const MainPage = () => {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === 'loading') return;
    if (!session) {
      router.push('/login');
    }
  }, [session, status, router]);

  useEffect(() => {
    const fetchAndRedirect = async () => {
      if (status === 'authenticated' && session?.user) {
        try {
          // Fetch chats for the user from your backend (Prisma/Next.js API)
          const res = await fetch('/api/chat', { method: 'GET' });
          if (!res.ok) throw new Error('Failed to fetch chats');
          const chats = await res.json();
          if (Array.isArray(chats) && chats.length > 0) {
            router.push(`/main/${chats[0].id}`);
          } else {
            // No chats, create a new chat document
            const newChatRes = await fetch('/api/chat/new/', { method: 'POST' });
            if (!newChatRes.ok) throw new Error('Failed to create new chat');
            const data = await newChatRes.json();
            if (data && data.id) {
              router.push(`/main/${data.id}`);
            } else {
              throw new Error('No chat id returned');
            }
          }
        } catch (err) {
          console.error('Error fetching or creating chat:', err);
        }
      }
    };
    fetchAndRedirect();
  }, [session, status, router]);

  if (status === 'loading' || !session) {
    return (
      <div className="flex items-center justify-center h-screen">
        <span className="text-gray-500 text-lg">Loading...</span>
      </div>
    );
  }

  return null;
};

export default MainPage;