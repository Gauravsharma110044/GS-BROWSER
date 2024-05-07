import { Chat, User } from '@prisma/client'
import { Menu } from 'lucide-react'
import React from 'react'
import { Sheet, SheetContent, SheetTrigger } from './ui/sheet'
import SideBar from './sidebar/SideBar'

interface MobileSidebarProps {
  chats: Chat[]
  user: User
}

const MobileSidebar = ({chats, user}: MobileSidebarProps) => {
  return (
    <Sheet>
      <SheetTrigger>
        <button className='px-2 py-2 mr-2 rounded-md hover:bg-zinc-700/30 transition md:hidden'>
          <Menu className='h-5 w-5 text-gray-300' />
        </button>
      </SheetTrigger>
      <SheetContent side='left' className='p-0 flex gap-0 border-0'>
        <SideBar />
      </SheetContent>
    </Sheet>
  )
}

export default MobileSidebar
