import SideBar from "@/components/sidebar/SideBar";
import { currentUser } from "@/lib/current-user";
import { redirect } from "next/navigation";

export default async function ChatLayout({children}: {children: React.ReactNode}){
  const user = await currentUser()
  if(!user){
    return redirect('/login')
  }
    
  return (
    <div className="h-full">
      <aside className="hidden md:flex h-full w-72 z-30 flex-col fixed inset-y-0">
        <SideBar />
      </aside>
      <main className="md:pl-72 h-full bg-[#212121]">
        {children}
      </main>
    </div>
  )
}