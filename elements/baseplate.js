class Baseplate {
    constructor(center, normal, radius, numberOfSegmentsCircumferential, numberOfSegmentsRadial) {
        this.triangles = [];

        for(let r = 0; r < numberOfSegmentsRadial; r++) {
            let segmentInsideRadius = radius
                .clone()
                .multiplyScalar(r / numberOfSegmentsRadial);
            let segmentOutsideRadius = radius
                .clone()
                .multiplyScalar((r + 1) / numberOfSegmentsRadial);
            for(let c = 0; c < numberOfSegmentsCircumferential; c++) {
                let segmentInsideRadius1 = segmentInsideRadius
                    .clone()
                    .applyAxisAngle(
                        normal.clone().normalize(), 
                        c / numberOfSegmentsCircumferential * 2 * Math.PI
                    );
                let segmentInsideRadius2 = segmentInsideRadius
                    .clone()
                    .applyAxisAngle(
                        normal.clone().normalize(), 
                        (c + 1) / numberOfSegmentsCircumferential * 2 * Math.PI
                    );
                let segmentOutsideRadius1 = segmentOutsideRadius
                    .clone()
                    .applyAxisAngle(
                        normal.clone().normalize(), 
                        c / numberOfSegmentsCircumferential * 2 * Math.PI
                    );
                let segmentOutsideRadius2 = segmentOutsideRadius
                    .clone()
                    .applyAxisAngle(
                        normal.clone().normalize(), 
                        (c + 1) / numberOfSegmentsCircumferential * 2 * Math.PI
                    );
                this.triangles.push(new Triangle(
                    (center.clone().add(segmentInsideRadius1)).toArray(),
                    (center.clone().add(segmentOutsideRadius1)).toArray(),
                    (center.clone().add(segmentOutsideRadius2)).toArray()
                ));
                if(r > 0) {
                    this.triangles.push(new Triangle(
                        (center.clone().add(segmentInsideRadius2)).toArray(),
                        (center.clone().add(segmentInsideRadius1)).toArray(),
                        (center.clone().add(segmentOutsideRadius2)).toArray()
                    ));
                }
            }

            this.lines = this.triangles.map(t => t.lines);
            this.faces = this.triangles.map(t => t.face);
        }
    }
}