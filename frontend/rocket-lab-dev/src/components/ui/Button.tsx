import type { ButtonHTMLAttributes, PropsWithChildren } from 'react'

type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement>, PropsWithChildren {
  variant?: ButtonVariant
}

const variantClasses: Record<ButtonVariant, string> = {
  primary: 'bg-[#b5e48c] text-white hover:bg-[#a3d97b]',
  secondary: 'bg-slate-100 text-slate-800 hover:bg-slate-200',
  danger: 'bg-rose-600 text-white hover:bg-rose-700',
  ghost: 'bg-transparent text-slate-700 hover:bg-slate-100',
}

export function Button({ variant = 'primary', className = '', children, ...props }: ButtonProps) {
  return (
    <button
      className={`inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-medium transition ${variantClasses[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}
