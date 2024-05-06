import { createNewChat } from "@/lib/chat"
import { currentUser } from "@/lib/current-user"
import prisma from "@/lib/prisma"
import { redirect } from "next/navigation"

const page = async () => {
  const user = await currentUser()
  const chats = await prisma.chat.findMany({
    where: {
      userId: user?.id
    },
    orderBy: {
      createdAt: 'desc'
    }
  })

  console.log(chats)
  if(chats.length === 0){
    console.log('creating new chat')
    await createNewChat()
  }
  return redirect(`/${chats[0]?.id}`)
}

export default page