import React from 'react'
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar'
import { cn } from '@/lib/utils'

interface UserAvatarProps {
  className?: string
}


const BotAvatar = ({className}: UserAvatarProps) => {
  return (
    <Avatar className={cn("h-7 w-7 md:h-8 md:w-8", className)}>
      <AvatarImage src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/768px-ChatGPT_logo.svg.png' alt="ChatGPT" />
      <AvatarFallback>ChatGPT</AvatarFallback>
    </Avatar>
  )
}

export default BotAvatar