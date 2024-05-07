import SideBar from "@/components/sidebar/SideBar";
import { currentUser } from "@/lib/current-user";
import prisma from "@/lib/prisma";
import { redirect } from "next/navigation";

export default async function ChatLayout({children}: {children: React.ReactNode}){
  const user = await currentUser()
  if(!user){
    return redirect('/login')
  }
  const chats = await prisma.chat.findMany({
    where: {
      userId: user.id
    }
  })
  if(!chats){
    return (
      <div>
        no chats found
      </div>
    )
  }
  return (
    <div className="h-full">
      <aside className="hidden md:flex h-full w-72 z-30 flex-col fixed inset-y-0">
        <SideBar user={user} chats={chats} />
      </aside>
      <main className="md:pl-72 h-full bg-[#212121]">
        {children}
      </main>
    </div>
  )
}