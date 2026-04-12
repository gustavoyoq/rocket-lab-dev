import { useEffect, useState } from 'react'
import { getProductDetailsById, listProductReviewsById, listProducts } from '../services/products'
import type { ProductListingItem, ProductReview } from '../types/product'

export function useProductDetails(productId: string | undefined) {
  const [product, setProduct] = useState<ProductListingItem | null>(null)
  const [reviews, setReviews] = useState<ProductReview[]>([])
  const [similarProducts, setSimilarProducts] = useState<ProductListingItem[]>([])
  const [similarLoading, setSimilarLoading] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (typeof productId !== 'string' || productId.trim() === '') {
      setError('Produto nao encontrado.')
      setLoading(false)
      setSimilarLoading(false)
      return
    }

    const currentProductId = productId

    async function loadProduct() {
      setLoading(true)
      setSimilarLoading(true)
      setError(null)

      try {
        const [productDetails, productReviews] = await Promise.all([
          getProductDetailsById(currentProductId),
          listProductReviewsById(currentProductId, { page: 1, pageSize: 30 }),
        ])

        setProduct(productDetails)
        setReviews(productReviews)

        try {
          const similarPage = await listProducts({
            page: 1,
            pageSize: 60,
            category: productDetails.categoria_produto,
          })

          setSimilarProducts(similarPage.items.filter((item) => item.id_produto !== currentProductId))
        } catch {
          setSimilarProducts([])
        }
      } catch {
        setError('Nao foi possivel carregar os detalhes do produto.')
      } finally {
        setLoading(false)
        setSimilarLoading(false)
      }
    }

    void loadProduct()
  }, [productId])

  return { product, reviews, similarProducts, similarLoading, loading, error }
}
