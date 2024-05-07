"use client"
import { Form, FormControl, FormField, FormItem } from "../ui/form"
import { Input } from "../ui/input"
import * as z from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from "react-hook-form"
import axios from "axios"
import { Chat } from "@prisma/client"
import { useEffect } from "react"
import { useRouter } from "next/navigation"

const FormSchema = z.object({
  name: z.string().min(1)
})

interface SideBarItemEditProps {
  chat: Chat
  setIsEditing: React.Dispatch<React.SetStateAction<boolean>>
}

export const SideBarItemEdit = ({chat, setIsEditing}: SideBarItemEditProps) => {
  const router = useRouter()
  useEffect(() => {
    const handleKeyDown = (event: any) => {
      if(event.key === 'Escape' || event.keyCode === 27){
        setIsEditing(false)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])
  
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      name: chat.name
    }
  })
  const isLoading = form.formState.isSubmitting

  const onSubmit = async (values: z.infer<typeof FormSchema>) => {
    try {
      await axios.patch(`/api/chat/${chat.id}`, values)
      form.reset()
      router.refresh()
    } catch (error) {
      console.log(error)
    } finally {
      setIsEditing(false)
    }
  }



  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className='flex items-center w-full gap-x-2 pt-2'>
        <FormField
          control={form.control}
          name='name'
          render={(({field}) => (
            <FormItem className='flex-1'>
              <FormControl>
                <div className='relative w-full'>
                  <Input autoFocus disabled={isLoading} placeholder='Edited Name...' {...field} className='px-2 bg-zinc-200/90 dark:bg-zinc-700/75 border-none border-0 focus-visible:ring-0 focus-visible:ring-offset-0 text-zinc-600 dark:text-zinc-200' />
                </div>
              </FormControl>
            </FormItem>
          ))}
        />
      </form>
    </Form>
  )
}