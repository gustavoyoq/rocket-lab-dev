import { forwardRef } from 'react'
import type { InputHTMLAttributes } from 'react'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {}

export const Input = forwardRef<HTMLInputElement, InputProps>(function Input({ className = '', ...props }, ref) {
  return (
    <input
      ref={ref}
      className={`w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-[#b5e48c] focus:ring-2 focus:ring-[#b5e48c]/20 ${className}`}
      {...props}
    />
  )
})
