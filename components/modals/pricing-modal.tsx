"use client"
import { useModal } from "@/hooks/use-modal-store"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button, buttonVariants } from "@/components/ui/button"
import { useState } from "react"
import { Separator } from "../ui/separator"
import axios from "axios"
import { useRouter } from "next/navigation"
import { cn } from "@/lib/utils"
import { Check } from "lucide-react"

const PLANS = [
  {
    "name": "Free",
    "price": "USD $0/month",
    "action": "Your current Plan",
    "description": "For people just getting started with ChatGPT",
    "features": [
      "Unlimited messages, interactions, and history",
      "Access to our GPT-3.5 model",
      "Access on Web, iOS, and Android"
    ]
  },
  {
    "name": "Plus",
    "price": "USD $20/month",
    "action": "Upgrade to Plus",
    "description": "Everything in Free, and:",
    "features": [
      "Access to GPT-4, our most capable model",
      "Browse, create, and use GPTs",
      "Access to additional tools like DALL·E, Browsing, Advanced Data Analysis and more"
    ]
  },
  {
    "name": "Team",
    "price": "USD $25 per person/month*",
    "action": "Upgrade to Team",
    "description": "Everything in Plus, and:",
    "features": [
      "Higher message caps on GPT-4 and tools like DALL·E, Browsing, Advanced Data Analysis, and more",
      "Create and share GPTs with your workspace",
      "Admin console for workspace management",
      "Team data excluded from training by default"
    ]
  }
]


export const PricingModal = () => {
  const router = useRouter()
  const {data, isOpen, onClose, onOpen, type} = useModal()
  const isModalOpen = isOpen && type === 'pricing'
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
      <DialogContent className="bg-[#2f2f2f] text-white px-10 min-w-[60%]">
        <DialogHeader className="pt-8 px-6">
            <DialogTitle className="text-2xl text-left font-bold">Upgrade your plan</DialogTitle>
            <Separator className="h-[1px] bg-gray-700 my-3 mt-5" />
        </DialogHeader>
        <div className="grid grid-cols-3 gap-5">
          {PLANS.map((plan, idx) => {
            return (
              <div className="px-5">
                <h3 className="font-bold text-xl">{plan.name}</h3>
                <p className="text-sm text-gray-300">{plan.price}</p>
                <Button className={cn("w-full my-5", plan.name === 'Team' && 'bg-blue-600 hover:bg-blue-600/80', plan.name === 'Free' && 'bg-slate-600 hover:bg-slate-600/80')} variant={'green'} disabled={plan.name === 'Free'}>{plan.action}</Button>
                <div className="text-sm">
                  <p className="my-2">{plan.description}</p>
                  <ul className="space-y-2">
                    {plan.features.map((feature) => {
                      return (<li className="flex space-x-3"><Check className="flex-shrink-0 w-4 h-4" /><span>{feature}</span></li>)
                    })}
                  </ul>
                </div>
              </div>
            )
          })}
        </div>
        <Separator className="h-[1px] bg-gray-700" />
        <p className="text-center text-sm">Need more capabilities? See <span className={cn(buttonVariants({variant: "link"}), 'cursor-pointer')}>ChatGPT Enterprise</span></p>
      </DialogContent>
    </Dialog>
  )
}