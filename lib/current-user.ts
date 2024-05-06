import { authOptions } from "@/app/api/auth/[...nextauth]/route"
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
  console.log(user)
  return user
}