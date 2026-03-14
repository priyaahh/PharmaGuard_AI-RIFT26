import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'https://pharmaguard-ai-poyn.onrender.com/api'

const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 60000,
})

// Add request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method.toUpperCase(), config.url)
    return config
  },
  (error) => Promise.reject(error)
)

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error('API Error:', error.response.status, error.response.data)
    } else if (error.request) {
      console.error('No response from API:', error.request)
    } else {
      console.error('Error:', error.message)
    }
    return Promise.reject(error)
  }
)

/**
 * Analyze VCF file and drug for pharmacogenomic risk
 * @param {File} vcfFile - VCF file from user upload
 * @param {string|string[]} drugs - Drug name(s) to analyze
 * @returns {Promise<Object>} Risk assessment results
 */
export const analyzePharmacogenomics = async (vcfFile, drugs) => {
  const formData = new FormData()
  formData.append('vcf_file', vcfFile)
  
  if (Array.isArray(drugs)) {
    drugs.forEach((drug) => formData.append('drugs', drug))
  } else {
    formData.append('drugs', drugs)
  }

  try {
    const response = await apiClient.post('/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to analyze pharmacogenomics')
  }
}

/**
 * Get list of supported drugs
 * @returns {Promise<string[]>} List of drug names
 */
export const getSupportedDrugs = async () => {
  try {
    const response = await apiClient.get('/drugs')
    return response.data.drugs || []
  } catch (error) {
    console.warn('Failed to fetch supported drugs, using defaults')
    return [
      'CODEINE',
      'WARFARIN',
      'CLOPIDOGREL',
      'SIMVASTATIN',
      'AZATHIOPRINE',
      'FLUOROURACIL',
    ]
  }
}

/**
 * Validate VCF file structure
 * @param {File} vcfFile - VCF file to validate
 * @returns {Promise<Object>} Validation result
 */
export const validateVCFFile = async (vcfFile) => {
  const formData = new FormData()
  formData.append('vcf_file', vcfFile)

  try {
    const response = await apiClient.post('/validate-vcf', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'VCF validation failed')
  }
}

/**
 * Get health check status
 * @returns {Promise<Object>} API health status
 */
export const getHealthStatus = async () => {
  try {
    const response = await apiClient.get('/health')
    return response.data
  } catch (error) {
    throw new Error('API is not available')
  }
}

export default apiClient
