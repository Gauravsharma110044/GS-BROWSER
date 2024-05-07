import React from 'react'
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar'
import { cn } from '@/lib/utils'

interface UserAvatarProps {
    src?: string
    className?: string
    name?: string
}

const UserAvatar = ({className, src, name}: UserAvatarProps) => {
  return (
    <Avatar className={cn("h-7 w-7 md:h-10 md:w-10", className)}>
      <AvatarImage src={src} alt="Profile Image" />
      {name && (<AvatarFallback>{name[0].toUpperCase() + name[1].toUpperCase()}</AvatarFallback>)}
    </Avatar>
  )
}

export default UserAvatar