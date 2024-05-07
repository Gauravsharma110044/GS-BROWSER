import { currentUser } from '@/lib/current-user'
import prisma from '@/lib/prisma'
import { redirect } from 'next/navigation'
import { ScrollArea } from '../ui/scroll-area'
import SideBarFooter from './sidebar-footer'
import SideBarHeader from './sidebar-header'
import SideBarItem from './sidebar-item'

export const dynamic = 'force-dynamic'

const SideBar = async () => {
  const user = await currentUser()
  if(!user){
    return redirect('/login')
  }
  const chats = await prisma.chat.findMany({
    where: {
      userId: user.id
    }
  })
  console.log(chats)
  return (
    <div className='relative flex flex-col px-3 py-3 h-full text-primary w-full dark:bg-[#171717] bg-[#f2f3f5]'>
      <SideBarHeader />

      <ScrollArea className='flex-1 my-5'>
        {chats.map((chat) => {
          return (<SideBarItem chat={chat} key={chat.id} />)
        })}
      </ScrollArea>

      <SideBarFooter user={user} />
    </div>
  )
}

export default SideBar
