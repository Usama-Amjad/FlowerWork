import React from 'react'

const Footer = () => {
  return (
    <div className=' py-[4%] max-w-[1000px] mx-auto my-auto'>
        <ul className='text-white grid grid-cols-[auto_auto_auto] gap-4 mb-8 justify-around cursor-pointer'>
            <li>Help Centre</li>
            <li>Term of Use</li>
            <li>Privacy</li>
            <li>Jobs</li>
            <li>Legal Notice</li>
            <li>Contact Us</li>
        </ul>
        <p className='flex justify-around text-gray-400'>
            1997-2024 Netflix, Inc.
        </p>
      
    </div>
  )
}

export default Footer
