'use client';

import { useAuth } from '@/providers/auth-provider';
import { useRouter } from 'next/navigation';
import ChatContainer from '@/components/chat/chat-container';
import React from 'react';

export default function Home() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  // Redirect to login if not authenticated and not loading
  React.useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  if (loading || !user) {
    return (
      <div className="flex items-center justify-center h-screen">
        <span className="text-gray-500 text-lg">Loading...</span>
      </div>
    );
  }

  const handleSignOut = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <div className="flex flex-col h-screen">
      <header className="border-b p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">Logged in as {user?.email}</span>
        </div>
        <button
          onClick={handleSignOut}
          className="px-4 py-2 text-sm text-red-600 hover:text-red-700"
        >
          Logout
        </button>
      </header>
      <main className="flex-1">
        <ChatContainer />
      </main>
    </div>
  );
}