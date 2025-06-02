"use client"
import { Button, buttonVariants } from '@/components/ui/button'
import { Form, FormControl, FormField, FormItem, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Separator } from '@/components/ui/separator'
import { toast } from '@/components/ui/use-toast'
import { cn } from '@/lib/utils'
import { zodResolver } from '@hookform/resolvers/zod'
import { signIn } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import React from 'react'
import { useForm } from 'react-hook-form'
import * as z from 'zod'
import { FcGoogle } from 'react-icons/fc'
import { AiFillGithub } from 'react-icons/ai'

const FormSchema = z.object({
  email: z.string().min(1, "Email is required!").email("Invalid email!"),
  password: z
    .string()
    .min(1, "Password is required!")
    .min(8, "Password must have than 8 characters!"),
})

const LoginPage = () => {
  const router = useRouter()
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  })
  
  const isLoading = form.formState.isSubmitting

  const onSubmit = async (values: z.infer<typeof FormSchema>) => {
    try {
      const result = await signIn('credentials', {
        email: values.email,
        password: values.password,
        redirect: false,
      })
      if (result?.error) {
        toast({
          title: "Error",
          description: "Invalid credentials",
          variant: "destructive",
        })
        return
      }
      router.push('/main')
      router.refresh()
    } catch (error) {
      console.log(error)
      toast({
        title: "Error",
        description: "Something went wrong",
        variant: "destructive",
      })
    }
  }

  const handleGoogleSignIn = async () => {
    try {
      await signIn('google', { callbackUrl: '/main' })
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to sign in with Google",
        variant: "destructive",
      })
    }
  }

  const handleGithubSignIn = async () => {
    try {
      await signIn('github', { callbackUrl: '/main' })
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to sign in with Github",
        variant: "destructive",
      })
    }
  }

  return (
    <div className='space-y-4'>
      <h3 className='font-bold text-3xl text-center'>Welcome Back</h3>
      <Form {...form}>
        <form className='space-y-5' onSubmit={form.handleSubmit(onSubmit)}>
          <FormField 
            control={form.control}
            name='email'
            render={({field}) => (
              <FormItem>
                <FormControl>
                  <Input disabled={isLoading} className='focus-visible:ring-0 focus-visible:ring-offset-0 focus:border-emerald-400' placeholder='Email Address' {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField 
            control={form.control}
            name='password'
            render={({field}) => (
              <FormItem>
                <FormControl>
                  <Input disabled={isLoading} className='focus-visible:ring-0 focus-visible:ring-offset-0 focus:border-emerald-400' placeholder='Password' type='password' {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button variant='green' type='submit' disabled={isLoading} className='w-full'>Sign In</Button>
        </form>
      </Form>
      <div className='text-center'>
        Don&apos;t have an account? <span onClick={() => router.push('/register')} className={cn(buttonVariants({variant: 'link'}), 'text-emerald-500 cursor-pointer')}>Sign Up</span>
      </div>
      <Separator className='h-[2px]' />
      <div className='space-y-2'>
        <Button
          type='button'
          onClick={handleGoogleSignIn}
          variant='outline'
          className='w-full flex items-center justify-center'
        >
          <FcGoogle className='mr-2 h-5 w-5' />
          Continue with Google
        </Button>
        <Button
          type='button'
          onClick={handleGithubSignIn}
          variant='outline'
          className='w-full flex items-center justify-center'
        >
          <AiFillGithub className='mr-2 h-5 w-5' />
          Continue with Github
        </Button>
      </div>
    </div>
  )
}

export default LoginPage
