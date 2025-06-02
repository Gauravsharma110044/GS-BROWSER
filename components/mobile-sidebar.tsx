import { User, Chat } from '@prisma/client'
import { Menu } from 'lucide-react'
import React from 'react'
import { Sheet, SheetContent, SheetTrigger } from './ui/sheet'
import SideBar from './sidebar/SideBar'

interface MobileSidebarProps {
  user: User
  chats: Chat[]
}

const MobileSidebar = ({user, chats}: MobileSidebarProps) => {
  return (
    <Sheet>
      <SheetTrigger>
        <button className='px-2 py-2 mr-2 rounded-md hover:bg-zinc-700/30 transition lg:hidden' aria-label="Open menu">
          <Menu className='h-5 w-5 text-gray-300' />
        </button>
      </SheetTrigger>
      <SheetContent side="left" className='p-0 flex gap-0 border-0'>
        <SideBar chats={chats} user={user} />
      </SheetContent>
    </Sheet>
  )
}

export default MobileSidebar
