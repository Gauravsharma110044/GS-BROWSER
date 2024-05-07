"use client"
import React from 'react'
import UserAvatar from '../user-avatar'
import { User } from '@prisma/client'
import { Book, LogOut, Settings, Sparkle } from 'lucide-react'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from '../ui/dropdown-menu'
import { signOut } from 'next-auth/react'
import { useModal } from '@/hooks/use-modal-store'

const SideBarFooter = ({user}: {user: User}) => {
  const {onOpen} = useModal()
  return (
    <div className='space-y-2'>
      <button className='group p-2 rounded-md flex items-center gap-x-3 w-full hover:bg-zinc-700/30 transition'>
        <Sparkle />
        <div onClick={() => onOpen('deleteChat')} className='flex flex-col items-start'>
          <p className='text-sm font-semibold'>Upgrade plan</p>
          <span className='text-xs text-gray-400'>Get GPT-4, DALL-E, and more</span>
        </div>
      </button>
      <DropdownMenu>
        <DropdownMenuTrigger className="focus:outline-none" asChild>
          <button className='group p-2 rounded-md flex items-center gap-x-3 w-full hover:bg-zinc-700/30 transition'>
            {user.name && (<UserAvatar className='md:h-10 md:w-10' name={user.name} />)}
            <p className='text-sm'>{user.name}</p>
          </button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className='text-xs font-medium space-y-[2px]'>
          <DropdownMenuItem className='px-3 p-2 text-sm cursor-pointer'>
            {user.email}
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem className='px-3 p-2 text-sm cursor-pointer'>
            <Book className='flex-shrink-0 w-5 h-5 text-zinc-500 dark:text-zinc-400 mr-2'/> Customize GPT
          </DropdownMenuItem>
          <DropdownMenuItem className='px-3 p-2 text-sm cursor-pointer'>
            <Settings className='flex-shrink-0 w-5 h-5 text-zinc-500 dark:text-zinc-400 mr-2'/> Settings
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem onClick={() => signOut()} className='px-3 p-2 text-sm cursor-pointer'>
            <LogOut className='flex-shrink-0 w-5 h-5 text-zinc-500 dark:text-zinc-400 mr-2'/> Logout
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}

export default SideBarFooter
