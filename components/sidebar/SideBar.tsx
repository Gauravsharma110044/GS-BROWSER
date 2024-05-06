"use client"
import React from 'react'
import SideBarHeader from './sidebar-header'
import { ScrollArea } from '../ui/scroll-area'
import { Button } from '../ui/button'
import SideBarFooter from './sidebar-footer'
import { Chat } from '@prisma/client'
import { useRouter } from 'next/navigation'

interface SideBarProps {
  chats: Chat[]
}

const SideBar = ({chats}: SideBarProps) => {
  const router = useRouter()
  return (
    <div className='relative flex flex-col px-3 py-3 h-full text-primary w-full dark:bg-[#171717] bg-[#f2f3f5]'>
      <SideBarHeader />

      <ScrollArea className='flex-1 px-3 my-5'>
        {chats.map((chat, idx) => {
          return (<Button key={idx} onClick={() => router.push(`/${chat.id}`)} variant='ghost' className='w-full'>{chat.name}</Button>)
        })}
      </ScrollArea>

      <SideBarFooter />
    </div>
  )
}

export default SideBar
