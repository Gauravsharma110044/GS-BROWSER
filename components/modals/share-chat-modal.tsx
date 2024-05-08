"use client"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { useModal } from "@/hooks/use-modal-store"
import { useOrigin } from "@/hooks/use-origin"
import { Check, Copy } from "lucide-react"
import { useState } from "react"
import { Input } from "../ui/input"
import { Separator } from "../ui/separator"

export const ShareChatModal = () => {
  const {data, isOpen, onClose, onOpen, type} = useModal()
  const isModalOpen = isOpen && type === 'shareChat'
  const {chat} = data

  const origin = useOrigin()
  const publicUrl = `${origin}/share/${chat?.id}`
  const [copied, setCopied] = useState(false)
  const onCopy = () => {
    navigator.clipboard.writeText(publicUrl)
    setCopied(true)

    setTimeout(() => {
      setCopied(false)
    }, 1000);
  }


  return(
    <Dialog open={isModalOpen} onOpenChange={onClose}>
      <DialogContent className="bg-[#2f2f2f] text-white p-0 overflow-hidden">
        <DialogHeader className="pt-8 px-6">
            <DialogTitle className="text-2xl text-left font-bold">Share Chat</DialogTitle>
            <Separator className="h-[1px] bg-gray-700 my-3" />
            <DialogDescription className="text-left text-zinc-300">
              Here is the public link for your chat.
            </DialogDescription>
        </DialogHeader>
        <div className="p-6">
          <div className="flex items-center mt-2 gap-x-2">
            <Input className="bg-[#2f2f2f] text-white border border-zinc-600 focus-visible:ring-0 focus-visible:ring-offset-0" value={publicUrl} />
            <Button variant='green' size='icon' onClick={onCopy}>{copied ? (<Check />) : (<Copy />)}</Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}