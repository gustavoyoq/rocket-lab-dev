import { cloneElement, isValidElement, type ButtonHTMLAttributes, type PropsWithChildren, type ReactElement } from 'react'

type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement>, PropsWithChildren {
  variant?: ButtonVariant
  asChild?: boolean
}

const variantClasses: Record<ButtonVariant, string> = {
  primary: 'bg-[#70b92f] text-white hover:bg-[#3f972f]',
  secondary: 'bg-[#70b92f] text-white hover:bg-[#3f972f]',
  danger: 'bg-rose-600 text-white hover:bg-rose-700',
  ghost: 'bg-transparent text-[#2f7f22] hover:bg-[#4DAC39]/15',
}

export function Button({ variant = 'primary', asChild = false, className = '', children, ...props }: ButtonProps) {
  const buttonClasses = `inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-medium transition ${variantClasses[variant]} ${className}`

  if (asChild && isValidElement(children)) {
    const child = children as ReactElement<{ className?: string }>

    return cloneElement(child, {
      className: [buttonClasses, child.props.className].filter(Boolean).join(' '),
    })
  }

  return (
    <button
      className={buttonClasses}
      {...props}
    >
      {children}
    </button>
  )
}
