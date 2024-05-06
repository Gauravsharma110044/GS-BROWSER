import SideBar from "@/components/SideBar";
import { currentUser } from "@/lib/current-user";

export default async function ChatLayout({children}: {children: React.ReactNode}){
  const user = await currentUser()
  
  return (
    <div className="h-full">
      <aside className="hidden md:flex h-full w-60 z-30 flex-col fixed inset-y-0">
        <SideBar />
      </aside>
      <main className="md:pl-60 h-full">
        {children}
      </main>
    </div>
  )
}