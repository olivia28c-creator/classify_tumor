import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Brain, Activity, Target, ArrowRight } from "lucide-react";

const stats = [
  { icon: Brain, label: "Architecture", value: "CNN (ResNet-based)" },
  { icon: Activity, label: "Training Data", value: "3,000+ pictures" },
  { icon: Target, label: "Accuracy", value: "~82%" },
];

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 opacity-5" style={{ background: "var(--hero-gradient)" }} />
        <div className="relative mx-auto max-w-4xl px-6 py-24 text-center">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-secondary px-4 py-1.5 text-sm font-medium text-secondary-foreground">
            <Brain className="h-4 w-4" />
            Tumor Classification API
          </div>
          <h1 className="mb-6 text-5xl font-bold tracking-tight text-foreground sm:text-6xl">
            Skin Tumor Classification
          </h1>
          <p className="mx-auto mb-12 max-w-2xl text-lg leading-relaxed text-muted-foreground">
            Powered by deep learning, this application classifies skin tumor images 
            into two categories: benign vs malignant, using a convolutional neural network trained on 
            thousands of medical images.
          </p>
        </div>
      </section>

      {/* Stats */}
      <section className="mx-auto -mt-8 max-w-4xl px-6">
        <div className="grid gap-4 sm:grid-cols-3">
          {stats.map(({ icon: Icon, label, value }) => (
            <div
              key={label}
              className="rounded-xl border border-border bg-card p-6 text-center transition-shadow hover:shadow-lg"
              style={{ boxShadow: "var(--card-shadow)" }}
            >
              <Icon className="mx-auto mb-3 h-8 w-8 text-primary" />
              <p className="text-sm font-medium text-muted-foreground">{label}</p>
              <p className="mt-1 text-xl font-semibold text-card-foreground">{value}</p>
            </div>
          ))}
        </div>
      </section>

      {/* About */}
      <section className="mx-auto max-w-3xl px-6 py-20">
        <h2 className="mb-6 text-2xl font-bold text-foreground">About the Model</h2>
        <div className="space-y-4 text-muted-foreground leading-relaxed">
        <p>
          The model is based on the <strong>ResNet18</strong> architecture, pre-trained 
          on ImageNet. The convolutional layers were frozen to leverage general image 
          feature recognition, and the final linear layer was fine-tuned for binary 
          tumor classification. Data augmentation such as resizing, random crops, and 
          horizontal flips were applied during training to improve generalization.
        </p>

        <p>
          Training was optimized using <strong>Adadelta</strong> and <strong>CrossEntropyLoss</strong>, 
          achieving approximately <strong>82% accuracy</strong> 
          on both training and test sets.  
        </p>

        <p>
          Simply upload a skin lesion image and the application will return the predicted 
          class along with a confidence score.
        </p>
        </div>

        <Button
          size="lg"
          className="mt-10 gap-2"
          onClick={() => navigate("/predict")}
        >
          Try Prediction
          <ArrowRight className="h-4 w-4" />
        </Button>
      </section>
    </div>
  );
};

export default Index;
