"use client"
import React from 'react'
import { Button } from "@/components/ui/button"
import { signIn } from 'next-auth/react'
import { GitHubIcon } from '@/components/Icons'

const GithubLoginButton = () => {
  return (
    <Button className='w-full' onClick={() => signIn('github')} variant='outline'><GitHubIcon className='mr-2 h-4 w-4 dark:text-white' />Continue With Github</Button>
  )
}

export default GithubLoginButton