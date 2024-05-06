import React from 'react'
import SideBarHeader from './sidebar-header'
import { ScrollArea } from '../ui/scroll-area'
import { Button } from '../ui/button'
import SideBarFooter from './sidebar-footer'

const SideBar = () => {
  return (
    <div className='relative flex flex-col px-3 py-3 h-full text-primary w-full dark:bg-[#171717] bg-[#f2f3f5]'>
      <SideBarHeader />

      <ScrollArea className='flex-1 px-3 my-5'>
        <Button variant='ghost' className='w-full'>Two Sum</Button>
      </ScrollArea>

      <SideBarFooter />
    </div>
  )
}

export default SideBar
