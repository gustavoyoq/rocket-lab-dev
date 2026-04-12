export function getCategoryLabel(category: string | null | undefined): string {
  const normalized = (category ?? '').trim()
  if (normalized === '' || normalized.toLowerCase() === 'sem_categoria') {
    return 'Sem categoria'
  }

  return normalized
}
