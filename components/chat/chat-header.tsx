'use client'

import React from 'react'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from '../ui/dropdown-menu'
import { ChevronDown, Menu, MessageCircleDashed, Share, Sparkles, Zap } from 'lucide-react'
import { Chat, User } from '@prisma/client'
import MobileSidebar from '../mobile-sidebar'

interface ChatHeaderProps {
  chats: Chat[]
  user: User
}

const ChatHeader = ({chats, user}: ChatHeaderProps) => {
  return (
    <div className='font-semibold px-3 py-2 flex items-center h-14 border-neutral-200 dark:border-neutral-800 border-b-2'>
      <MobileSidebar chats={chats} user={user} />
      <div>
        <DropdownMenu>
          <DropdownMenuTrigger className="focus:outline-none" asChild>
            <button className='group p-2 px-4 rounded-md flex items-center gap-x-3 w-full hover:bg-zinc-700/30 transition'>
              <p className='text-xl'><span className='font-bold'>GoogleGPT </span><span className='text-gray-400'>3.5</span></p>
              <ChevronDown className="text-gray-400 h-5 w-5" />
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className='text-xs font-medium space-y-[2px]'>
            <DropdownMenuItem className='px-3 p-2 text-sm cursor-pointer'>
              <Zap className='flex-shrink-0 w-5 h-5 text-zinc-500 dark:text-zinc-400 mr-2'/> GPT-3.5
            </DropdownMenuItem>
            <DropdownMenuItem className='px-3 p-2 text-sm cursor-pointer'>
              <Sparkles className='flex-shrink-0 w-5 h-5 text-zinc-500 dark:text-zinc-400 mr-2'/> GPT-4
            </DropdownMenuItem>
            <DropdownMenuItem className='px-3 p-2 text-sm cursor-pointer'>
              <MessageCircleDashed className='flex-shrink-0 w-5 h-5 text-zinc-500 dark:text-zinc-400 mr-2'/> Temporary chat
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem className='px-3 p-2 text-sm cursor-pointer'>
              <Share className='flex-shrink-0 w-5 h-5 text-zinc-500 dark:text-zinc-400 mr-2'/> Share chat
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  )
}

export default ChatHeader