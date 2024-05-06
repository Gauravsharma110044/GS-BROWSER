import SideBar from "@/components/sidebar/SideBar";
import { currentUser } from "@/lib/current-user";

export default async function ChatLayout({children}: {children: React.ReactNode}){
  const user = await currentUser()
    
  return (
    <div className="h-full">
      <aside className="hidden md:flex h-full w-72 z-30 flex-col fixed inset-y-0">
        <SideBar />
      </aside>
      <main className="md:pw-72 h-full bg-[#212121]">
        {children}
      </main>
    </div>
  )
}