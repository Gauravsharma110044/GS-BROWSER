import { createNewChat } from "@/lib/chat"
import { currentUser } from "@/lib/current-user"
import prisma from "@/lib/prisma"
import { redirect } from "next/navigation"

const page = async () => {
  const user = await currentUser()
  if(!user){
    return redirect('/login')
  }
  const chats = await prisma.chat.findMany({
    where: {
      userId: user.id
    },
    orderBy: {
      createdAt: 'desc'
    }
  })

  if(chats.length === 0){
    const chat = await createNewChat()
    if(!chat){
      return null
    }
    return redirect(`/${chat.id}`)
  }else{
    return redirect(`/${chats[0]?.id}`)
  }
}

export default page