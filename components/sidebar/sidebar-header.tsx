import logoSvg from '@/public/logo.svg'
import { Chat } from '@prisma/client'
import axios from "axios"
import { Edit } from "lucide-react"
import Image from "next/image"
import { redirect, useRouter } from 'next/navigation'

const SideBarHeader = () => {
  const router = useRouter()
  const createChat = async () => {
    const response = await axios.post('api/chat/new')
    const chat = response.data
    console.log(chat)
    return router.push(`/${chat.id}`)
  }
  return (
    <button onClick={createChat} className='group px-2 py-2 rounded-md flex items-center gap-x-2 w-full hover:bg-zinc-700/30 transition'>
      <Image width={30} src={logoSvg} alt='logo' style={{stroke: 'red'}} />
      <p className='font-semibold text-sm'>New Chat</p>
      <Edit className="ml-auto w-5 h-5 mr-2"/>
    </button>
  )
}

export default SideBarHeader
