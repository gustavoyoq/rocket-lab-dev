import type { SelectHTMLAttributes } from 'react'

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {}

export function Select({ className = '', ...props }: SelectProps) {
  return (
    <select
      className={`w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-[#b5e48c] focus:ring-2 focus:ring-[#b5e48c]/20 ${className}`}
      {...props}
    />
  )
}
