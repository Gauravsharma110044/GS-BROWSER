import { currentUser } from "./current-user"
import prisma from "./prisma"

export const createNewChat = async () => {
  const user = await currentUser()
  const chat = await prisma.chat.create({
    data: {
      userId: user?.id as string,
      name: 'New Chat'
    }
  })
  return chat
}