"use client"
import axios from "axios"
import { Edit } from "lucide-react"
import { useRouter } from 'next/navigation'
import BotAvatar from '../bot-avatar'

const SideBarHeader = () => {
  const router = useRouter()
  const createChat = async () => {
    const response = await axios.post('api/chat/new')
    const chat = response.data
    router.push(`/${chat.id}`)
    router.refresh()
  }
  return (
    <button onClick={createChat} className='group px-2 py-2 rounded-md flex items-center gap-x-2 w-full hover:bg-zinc-700/30 transition'>
      <BotAvatar className='h-4 w-4' />
      <p className='font-semibold text-sm'>New Chat</p>
      <Edit className="ml-auto w-5 h-5 mr-2"/>
    </button>
  )
}

export default SideBarHeader
