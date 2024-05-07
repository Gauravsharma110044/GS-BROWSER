"use client"
import { useModal } from "@/hooks/use-modal-store"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { Separator } from "../ui/separator"
import axios from "axios"
import { useRouter } from "next/navigation"

export const DeleteChatModal = () => {
  const router = useRouter()
  const {data, isOpen, onClose, onOpen, type} = useModal()
  const isModalOpen = isOpen && type === 'deleteChat'
  const [isLoading, setIsLoading] = useState(false)
  const {chat} = data
  const onDelete = async () => {
    try {
      setIsLoading(true)
      await axios.delete(`/api/chat/${chat?.id}`)
      onClose()
      router.push('/')
      router.refresh()
    } catch (error) {
      console.log(error)
    } finally {
      setIsLoading(false)
    }
  }

  return(
    <Dialog open={isModalOpen} onOpenChange={onClose}>
      <DialogContent className="bg-[#2f2f2f] text-white p-0 overflow-hidden">
        <DialogHeader className="pt-8 px-6">
            <DialogTitle className="text-2xl text-left font-bold">Delete Chat?</DialogTitle>
            <Separator className="h-[1px] bg-gray-700 my-3" />
            <DialogDescription className="text-left text-zinc-300">
              Are you sure you want to delete <span className="font-bold text-white">{chat?.name}</span>?. <br />
              This action cannot be undone.
            </DialogDescription>
        </DialogHeader>
        <DialogFooter className="px-6 py-4">
          <div className="flex items-leftext-left justify-between w-full">
            <Button variant='ghost' disabled={isLoading} onClick={onClose}>Cancel</Button>
            <Button variant='destructive' disabled={isLoading} onClick={onDelete}>Confirm</Button>
          </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}