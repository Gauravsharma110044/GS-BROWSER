import ChatContent from '@/components/chat/chat-content'
import ChatHeader from '@/components/chat/chat-header'
import ChatInput from '@/components/chat/chat-input'
import ShareChatButton from '@/components/share-chat-button'
import { useSession } from 'next-auth/react'
import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { CircleHelp } from 'lucide-react'

const ChatPage = () => {
  const { data: session, status } = useSession()
  const router = useRouter()
  const params = useParams()
  const chatId = params?.chatId
  const [chat, setChat] = useState<any>(null)
  const [chats, setChats] = useState<any[]>([])
  const [chatLoading, setChatLoading] = useState(true)

  useEffect(() => {
    if (status === 'loading') return
    if (!session) {
      router.push('/login')
    }
  }, [session, status, router])

  useEffect(() => {
    const fetchChat = async () => {
      if (status === 'authenticated' && session?.user && chatId) {
        try {
          // Fetch all chats for sidebar/header
          const res = await fetch('/api/chat', { method: 'GET' })
          if (!res.ok) throw new Error('Failed to fetch chats')
          const chatsData = await res.json()
          setChats(chatsData)

          // Fetch the specific chat
          const chatRes = await fetch(`/api/chat/${chatId}`, { method: 'GET' })
          if (!chatRes.ok) {
            router.push('/main')
            return
          }
          const chatData = await chatRes.json()
          setChat(chatData)
        } catch (err) {
          console.error('Error loading chat:', err)
          router.push('/main')
        } finally {
          setChatLoading(false)
        }
      }
    }
    fetchChat()
  }, [session, status, chatId, router])

  if (status === 'loading' || chatLoading || !session) {
    return (
      <div className='flex items-center justify-center h-screen'>
        <span className='text-gray-500 text-lg'>Loading chat...</span>
      </div>
    )
  }

  return (
    <div className='flex flex-col h-full'>
      <ChatHeader chats={chats} user={session.user} />
      <div className='flex flex-1 overflow-y-auto container no-scrollbar lg:px-[14rem]'>
        <ChatContent chat={chat} />
      </div>
      <div className='container lg:px-[12rem]'>
        <ChatInput chat={chat} />
        <span className='flex justify-center mb-3 text-xs text-gray-300 text-center'>GoogleGPT can make mistakes. Consider checking important information.</span>
      </div>

      <ShareChatButton chat={chat} />
      <button className='absolute bottom-6 right-6' title='Help'>
        <CircleHelp className='h-5 w-5 text-gray-300' />
      </button>
    </div>
  )
}

export default ChatPage
