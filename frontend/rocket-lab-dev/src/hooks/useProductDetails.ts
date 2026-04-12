import { useEffect, useState } from 'react'
import { getProductDetailsById, listProductReviewsById } from '../services/products'
import type { ProductListingItem, ProductReview } from '../types/product'

export function useProductDetails(productId: string | undefined) {
  const [product, setProduct] = useState<ProductListingItem | null>(null)
  const [reviews, setReviews] = useState<ProductReview[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (typeof productId !== 'string' || productId.trim() === '') {
      setError('Produto nao encontrado.')
      setLoading(false)
      return
    }

    const currentProductId = productId

    async function loadProduct() {
      setLoading(true)
      setError(null)

      try {
        const [productDetails, productReviews] = await Promise.all([
          getProductDetailsById(currentProductId),
          listProductReviewsById(currentProductId, { page: 1, pageSize: 30 }),
        ])

        setProduct(productDetails)
        setReviews(productReviews)
      } catch {
        setError('Nao foi possivel carregar os detalhes do produto.')
      } finally {
        setLoading(false)
      }
    }

    void loadProduct()
  }, [productId])

  return { product, reviews, loading, error }
}
