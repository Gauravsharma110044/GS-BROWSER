import React from 'react'
import { Button } from "@/components/ui/button"
import { signIn } from 'next-auth/react'
import { GoogleIcon } from '@/components/Icons'

const GoogleLoginButton = () => {
  return (
    <Button className='w-full' onClick={() => signIn('google')} variant='outline'><GoogleIcon className='mr-2 h-4 w-4 dark:text-white' />Continue With Google</Button>
  )
}

export default GoogleLoginButton
