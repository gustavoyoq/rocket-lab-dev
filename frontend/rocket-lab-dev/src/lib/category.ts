export function getCategoryLabel(category: string | null | undefined): string {
  const normalized = (category ?? '').trim()
  if (normalized === '' || normalized.toLowerCase() === 'sem_categoria') {
    return 'Sem categoria'
  }

  return normalized
    .replace(/[_-]+/g, ' ')
    .split(/\s+/)
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
}
