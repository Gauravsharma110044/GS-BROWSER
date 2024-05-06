import { getServerSession } from 'next-auth'
import React from 'react'
import { authOptions } from '../api/auth/[...nextauth]/route'
import { redirect } from 'next/navigation'

const page = async () => {
  const session = await getServerSession(authOptions)
  if(!session){
    return redirect('/login')
  }
  return (
    <div>
      chat
    </div>
  )
}

export default page
