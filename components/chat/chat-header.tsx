import React from 'react'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from '../ui/dropdown-menu'
import { ChevronDown } from 'lucide-react'

const ChatHeader = () => {
  return (
    <div className='font-semibold px-3 py-2 flex items-center h-14 border-neutral-200 dark:border-neutral-800 border-b-2'>
      <div>
        <DropdownMenu>
          <DropdownMenuTrigger className="focus:outline-none" asChild>
            <button className='group p-2 px-4 rounded-md flex items-center gap-x-3 w-full hover:bg-zinc-700/30 transition'>
              <p className='text-xl'><span className='font-bold'>ChatGPT </span>3.5</p>
              <ChevronDown className="text-gray-300 h-5 w-5 ml-auto" />
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className='text-xs font-medium space-y-[2px]'>
            <DropdownMenuItem className='px-3 p-2 text-sm cursor-pointer'>
              chauhanchetan12789@gmail.com
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem className='px-3 p-2 text-sm cursor-pointer'>
              {/* <Book className='flex-shrink-0 w-5 h-5 text-zinc-500 dark:text-zinc-400 mr-2'/> Customize GPT */}
            </DropdownMenuItem>
            <DropdownMenuItem className='px-3 p-2 text-sm cursor-pointer'>
              {/* <Settings className='flex-shrink-0 w-5 h-5 text-zinc-500 dark:text-zinc-400 mr-2'/> Settings */}
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem className='px-3 p-2 text-sm cursor-pointer'>
              {/* <LogOut className='flex-shrink-0 w-5 h-5 text-zinc-500 dark:text-zinc-400 mr-2'/> Logout */}
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  )
}

export default ChatHeader