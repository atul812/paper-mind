import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'https://didactic-dollop-wrqpjx6q79jvhg944-8000.app.github.dev/',
  timeout: 120000, // Increased timeout to 2 minutes
  headers: {
    'Content-Type': 'application/json',
  },
})

export async function runPipeline(query) {
  console.log('[API] PIPELINE_START:', { query })
  console.time('fetch')

  try {
    const response = await apiClient.post('/api/pipeline', { query })
    console.timeEnd('fetch')
    console.log('[API] RAW_RESPONSE:', response.status, response.data)

    const payload = response.data

    if (!payload) {
      throw new Error('Empty response from backend')
    }

    if (payload.error) {
      console.error('[API] ERROR_RESPONSE:', payload.error)
      throw new Error(payload.error)
    }

    // Extract data from wrapper
    const data = payload.data || payload
    console.log('[API] EXTRACTED_DATA:', {
      keys: Object.keys(data),
      paperCount: data.papers?.length ?? 0,
      velocityCount: data.velocity?.length ?? 0,
      momentumCount: data.momentum?.length ?? 0,
      forecastCount: data.forecast?.length ?? 0,
      topicMapSize: Object.keys(data.topic_map || {}).length,
    })

    // Validate required fields exist
    const requiredFields = ['papers', 'topic_map', 'velocity', 'citation_velocity', 'momentum', 'forecast', 'top_accelerating']
    const missingFields = requiredFields.filter((field) => !(field in data))

    if (missingFields.length > 0) {
      console.warn('[API] MISSING_FIELDS:', missingFields)
    }

    // Ensure all fields exist (with empty fallbacks)
    const validatedData = {
      papers: Array.isArray(data.papers) ? data.papers : [],
      topic_map: typeof data.topic_map === 'object' && data.topic_map !== null ? data.topic_map : {},
      tfidf_matrix: Array.isArray(data.tfidf_matrix) ? data.tfidf_matrix : [],
      velocity: Array.isArray(data.velocity) ? data.velocity : [],
      citation_velocity: Array.isArray(data.citation_velocity) ? data.citation_velocity : [],
      momentum: Array.isArray(data.momentum) ? data.momentum : [],
      forecast: Array.isArray(data.forecast) ? data.forecast : [],
      top_accelerating: Array.isArray(data.top_accelerating) ? data.top_accelerating : [],
    }

    console.log('[API] VALIDATED_DATA:', validatedData)
    return validatedData
  } catch (error) {
    console.error('[API] FETCH_ERROR:', error.message, error)
    throw error
  }
}
