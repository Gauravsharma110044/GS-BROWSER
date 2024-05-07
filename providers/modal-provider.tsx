"use client"

import { DeleteChatModal } from "@/components/modals/delete-chat-modal"
import { ShareChatModal } from "@/components/modals/share-chat-modal"
import { useEffect, useState } from "react"

export const ModalProvider = () => {
  const [isMounted, setIsMounted] = useState(false)
  useEffect(() => {
      setIsMounted(true)
  }, [])

  if(!isMounted){
      return null
  }
  return (
    <>
      <DeleteChatModal />
      <ShareChatModal />
    </>
  )
}