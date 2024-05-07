import {authOptions} from '@/lib/authOptions'
import { getServerSession } from "next-auth"
import prisma from "./prisma"

export const currentUser = async () => {
  const session = await getServerSession(authOptions)
  if(!session){
    return null
  }

  const user = await prisma.user.findUnique({
    where: {
      id: session.user?.id
    }
  })
  if(!user){
    return null
  }
  return user
}