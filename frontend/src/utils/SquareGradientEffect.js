import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export default function SquareBoxEffect(...inputs) {
  return twMerge(clsx(inputs))
}
