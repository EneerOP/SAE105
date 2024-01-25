<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\BinaryFileResponse;

class PythonController extends AbstractController
{
    #[Route('/exec', name: 'app_exec')]
    public function base(Request $request): Response
    {
        // Exécution du script Python si le formulaire est soumis
        if ($request->isMethod('POST')) {
            $this->executePythonCode();

            // Vérifier si le fichier HTML existe
            if (file_exists('test.html')) {
                // Lire le contenu HTML généré
                $htmlContent = file_get_contents('test.html');
            }
        }

        // Charger les 10 premières lignes du fichier CSV
        $csvData = $this->loadFirstTenRows('test.csv');

        // Passage du contenu HTML généré et les 10 premières lignes du CSV au modèle Twig
        return $this->render('base.html.twig', [
            'html_content' => $htmlContent ?? null,
            'csv_data' => $csvData,
        ]);
    }

    // Fonction pour exécuter le script Python
    private function executePythonCode(): void
    {
        // Exécution du script Python
        $output = shell_exec('python code-extraction 2>&1');
        
        // Afficher la sortie (utile pour le débogage)
        var_dump($output);
    }

    // Fonction pour charger les 10 premières lignes du fichier CSV
    private function loadFirstTenRows(string $filePath): array
    {
        $csvData = [];
        if (($handle = fopen($filePath, 'r')) !== false) {
            $count = 0;
            while (($row = fgetcsv($handle, 1000, ';')) !== false && $count < 15) {
                $csvData[] = $row;
                $count++;
            }
            fclose($handle);
        }

        return $csvData;
    }

    #[Route("/download-csv", name: "download_csv")]
    public function downloadCsv(): Response
    {
    $csvFilePath = $this->getParameter('kernel.project_dir') . '/public/test.csv';

    $response = new BinaryFileResponse($csvFilePath);
    $response->headers->set('Content-Type', 'application/csv');
    $response->headers->set('Content-Disposition', 'attachment; filename="resultats.csv"');

    return $response;
}

}
