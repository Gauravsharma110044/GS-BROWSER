import { currentUser } from "./current-user"
import prisma from "./prisma"

export const createNewChat = async () => {
  const user = await currentUser()
  if(!user){
    return null
  }
  const chat = await prisma.chat.create({
    data: {
      userId: user.id,
      name: 'New Chat'
    }
  })
  return chat
}