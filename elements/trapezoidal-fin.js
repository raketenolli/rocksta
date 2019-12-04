class TrapezoidalFin {
    constructor(rootTip, rootEnd, semiSpan, tipChord, sweep, numberOfSegmentsChordwise, numberOfSegmentsSpanwise) {
        this.triangles = [];
        this.rootVector = new THREE.Vector3().subVectors(rootEnd, rootTip);
        this.rootChord = this.rootVector.length();
        this.sweepVector = this.rootVector.clone().multiplyScalar(sweep / this.rootVector.length());
        console.log(`rootChord: ${this.rootChord}`);
        console.log(`tipChord ${tipChord}`);
        for(let s = 0; s < numberOfSegmentsSpanwise; s++) {
            let stripInsideTip = rootTip
                .clone()
                .add(semiSpan.clone().multiplyScalar(s / numberOfSegmentsSpanwise))
                .add(this.sweepVector.clone().multiplyScalar(s / numberOfSegmentsSpanwise));
            let stripOutsideTip = rootTip
                .clone()
                .add(semiSpan.clone().multiplyScalar((s + 1) / numberOfSegmentsSpanwise))
                .add(this.sweepVector.clone().multiplyScalar((s + 1) / numberOfSegmentsSpanwise));
            console.log(`s: ${s}`);
            console.log(`stripInsideTip: ${JSON.stringify(stripInsideTip)}`);
            console.log(`stripOutsideTip: ${JSON.stringify(stripOutsideTip)}`);
            let elementInsideChord = (this.rootChord + (s / numberOfSegmentsSpanwise) * (tipChord - this.rootChord)) / numberOfSegmentsChordwise;
            let elementOutsideChord = (this.rootChord + ((s + 1) / numberOfSegmentsSpanwise) * (tipChord - this.rootChord)) / numberOfSegmentsChordwise;
            console.log(`insideChord: ${elementInsideChord}`);
            console.log(`outsideChord: ${elementOutsideChord}`);
            for(let c = 0; c < numberOfSegmentsChordwise; c++) {
                let elementInsideTip = stripInsideTip
                    .clone()
                    .add(this.rootVector.clone().normalize().multiplyScalar(elementInsideChord).multiplyScalar(c));
                let elementInsideEnd = stripInsideTip
                    .clone()
                    .add(this.rootVector.clone().normalize().multiplyScalar(elementInsideChord).multiplyScalar(c + 1));
                let elementOutsideTip = stripOutsideTip
                    .clone()
                    .add(this.rootVector.clone().normalize().multiplyScalar(elementOutsideChord).multiplyScalar(c));
                let elementOutsideEnd = stripOutsideTip
                    .clone()
                    .add(this.rootVector.clone().normalize().multiplyScalar(elementOutsideChord).multiplyScalar(c + 1));
                this.triangles.push(new Triangle(
                    elementInsideTip.toArray(),
                    elementInsideEnd.toArray(),
                    elementOutsideEnd.toArray()
                ));
                this.triangles.push(new Triangle(
                    elementInsideTip.toArray(),
                    elementOutsideEnd.toArray(),
                    elementOutsideTip.toArray()
                ));
            }
        }

        this.lines = this.triangles.map(t => t.lines);
        this.faces = this.triangles.map(t => t.face);
    }
}